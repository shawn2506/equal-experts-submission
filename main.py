#!/usr/bin/env python3

"""
Author : Shawn Dsouza (Converted to FastAPI)
Date   : 2025-11-16
Script Name: main.py
Description: This script starts a FastAPI server locally serving on port 8080.
             Under the hood, it asynchronously calls the 
             https://api.github.com/users/{username}/gists URL.
             It resolves requests for the respective GitHub users you wish to test.
             Examples: http://localhost:8080/{usename}

Usage:
    - Install dependencies:
      $ pip install --no-cache-dir -r requirements.txt
    - Run the script:
      $ uv run uvicorn main:app --reload --port 8080
    - To check the execution, use any browser or curl:
    Examples:
      $ curl http://localhost:8080/octocat
      $ curl http://localhost:8080/shawn2506
"""

from typing import List, Optional
import uvicorn
import httpx
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

### Define Data Models (with Pydantic) ---
# This describes the *output* data structure, giving you
# automatic data validation and an OpenAPI (Swagger) schema.


class GistFile(BaseModel):
    """
    Represents a single file within a GitHub Gist.
    Attributes:
        filename (str | None): The name of the file.
        type (str | None): The MIME type of the file.
        language (str | None): The programming language detected for the file.
        raw_url (str | None): URL to access the raw file content.
        size (int | None): File size in bytes.
    """
    filename: Optional[str]
    type: Optional[str]
    language: Optional[str]
    raw_url: Optional[str]
    size: Optional[int]

class Gist(BaseModel):
    """
    Represents a GitHub Gist and its associated metadata.
    Attributes:
        id (str | None): The unique identifier of the gist.
        login (str | None): The username of the gist owner.
        owner_id (int | None): The numeric ID of the gist owner.
        description (str | None): A short text description of the gist.
        url (str | None): The API URL referencing this gist.
        created_at (str | None): Timestamp when the gist was created (ISO8601 format).
        updated_at (str | None): Timestamp when the gist was last updated (ISO8601 format).
        public (bool | None): Whether the gist is publicly visible.
        files (List[GistFile]): A list of files included in the gist.
        comments (int | None): Number of comments on the gist.
    """
    id: Optional[str]
    login: Optional[str]
    owner_id: Optional[int]
    description: Optional[str]
    url: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    public: Optional[bool]
    files: List[GistFile]
    comments: Optional[int]

### Create the FastAPI App Instance ---
app = FastAPI(
    title="GitHub Gist Proxy",
    description="A FastAPI service to proxy GitHub Gists for a user.",
    version="1.0.0"
)

### Create the API Endpoint ---

@app.get(
    "/{username}",
    response_model=List[Gist],  # Defines the successful output structure
    summary="Get Gists for a User",
    responses={
        404: {"description": "Error: Gists not found or user does not exist."}
    }
)
async def get_user_gists(username: str, response: Response):
    """
    Fetches all gists for a given GitHub username.
    
    - **username**: The GitHub username (e.g., "octocat").
    """
    gists_url = f"https://api.github.com/users/{username}/gists"
    ### Use httpx.AsyncClient for non-blocking network calls
    async with httpx.AsyncClient() as client:
        try:
            gh_response = await client.get(gists_url, timeout=60)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Error contacting GitHub API: {exc}"
            ) from exc

    ### Replicate original logic: fail if status is not 200
    if gh_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Error: Gists not found or user does not exist."
        )

    gists_data = gh_response.json()

    ### Replicate original logic: fail if the resulting JSON list is empty
    if not gists_data:
        raise HTTPException(
            status_code=404,
            detail="Error: Gists not found or user does not exist."
        )

    ### Transform Data ---
    gist_list = []
    for gist in gists_data:
        owner = gist.get("owner", {}) # Use .get() for safety

        # Transform files
        files_list = []
        for file_info in gist.get("files", {}).values():
            files_list.append(
                GistFile(  # Use the Pydantic model
                    filename=file_info.get("filename"),
                    type=file_info.get("type"),
                    language=file_info.get("language"),
                    raw_url=file_info.get("raw_url"),
                    size=file_info.get("size")
                )
            )
        ### Create the Gist object
        gist_list.append(
            Gist(  # Use the Pydantic model
                id=gist.get("id"),
                login=owner.get("login"),
                owner_id=owner.get("id"),
                description=gist.get("description", "No description") or "No description",
                url=gist.get("html_url"),
                created_at=gist.get("created_at"),
                updated_at=gist.get("updated_at"),
                public=gist.get("public"),
                files=files_list,
                comments=gist.get("comments")
            )
        )

    ### Set the cache header, just like in the original
    response.headers["Cache-Control"] = "public, max-age=3600"
    return gist_list

### Add a Root Endpoint (Good Practice) ---
@app.get("/")
async def read_root():
    """
    A simple root endpoint to confirm the server is running.
    """
    return {
        "message": "Server running. Try /octocat or /docs for API documentation."
    }

### Run the Server ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
