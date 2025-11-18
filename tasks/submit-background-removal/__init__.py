#region generated meta
import typing
class Inputs(typing.TypedDict):
    imageURL: str

class Outputs(typing.TypedDict):
    request_id: str
#endregion

from oocana import Context
import requests

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Submit an image to the background removal API.

    Args:
        params: Input parameters containing the image URL
        context: OOMOL context for accessing API token

    Returns:
        Dictionary containing the request_id for tracking the job
    """
    url = "https://fusion-api.oomol.com/v1/fal-remove-background/submit"

    # Get OOMOL token
    token = await context.oomol_token()

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "imageURL": params["imageURL"]
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()

    # The API returns sessionID
    request_id = result.get("sessionID", "")

    if not request_id:
        raise Exception(f"No sessionID found in API response: {result}")

    return {"request_id": request_id}
