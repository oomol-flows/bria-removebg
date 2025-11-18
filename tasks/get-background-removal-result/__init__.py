#region generated meta
import typing
class Inputs(typing.TypedDict):
    request_id: str
    max_retries: float | None
    retry_interval: float | None
class Outputs(typing.TypedDict):
    result_url: typing.NotRequired[str]
    status: typing.NotRequired[str]
#endregion

from oocana import Context
import requests
import time

async def main(params: Inputs, context: Context) -> Outputs:
    """
    Poll the background removal API to get the processed image result.

    Args:
        params: Input parameters containing request_id and polling configuration
        context: OOMOL context for accessing API token

    Returns:
        Dictionary containing the result_url and status
    """
    request_id = params["request_id"]
    max_retries = params.get("max_retries", 30)
    retry_interval = params.get("retry_interval", 2)

    url = f"https://fusion-api.oomol.com/v1/fal-remove-background/result/{request_id}"

    # Get OOMOL token
    token = await context.oomol_token()

    headers = {
        "Authorization": token
    }

    for attempt in range(max_retries):
        # Report progress
        progress = int((attempt + 1) / max_retries * 100)
        context.report_progress(progress)

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()

        # Print the API response to understand its structure
        print(f"Attempt {attempt + 1}: API Response: {result}")

        # API returns 'state' field, not 'status'
        state = result.get("state", "unknown")
        success = result.get("success", False)

        # Check if we have the result data (successful completion)
        if "data" in result and "image" in result["data"]:
            image_url = result["data"]["image"].get("url", "")
            print(f"Job completed successfully! Image URL: {image_url}")
            return {
                "result_url": image_url,
                "status": "completed"
            }
        # Check if still processing
        elif state == "processing":
            print(f"Job is still processing, waiting {retry_interval}s before retry...")
            if attempt < max_retries - 1:
                time.sleep(retry_interval)
        # Check for failure
        elif not success or state == "failed":
            print(f"Job failed: {result}")
            raise Exception(f"Background removal job failed: {result.get('error', 'Unknown error')}")
        else:
            # Unknown state, print and wait
            print(f"Unknown state '{state}', full response: {result}")
            if attempt < max_retries - 1:
                time.sleep(retry_interval)

    # If we've exhausted all retries
    raise Exception(f"Background removal job timed out after {max_retries} attempts")
