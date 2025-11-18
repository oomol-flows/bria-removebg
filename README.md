# BRIA Background Removal

A powerful OOMOL package for removing backgrounds from images using the BRIA AI background removal API. This package provides both URL-based and file-based workflows to seamlessly integrate background removal into your image processing pipelines.

## Features

- Remove backgrounds from images via URL
- Remove backgrounds from local image files
- Automatic cloud upload and download
- Configurable polling for job completion
- Easy-to-use subflow blocks

## Subflows

This package includes two main subflows for different use cases:

### 1. URL Image Background Removal

Remove background from an image URL and return the processed image URL.

**Inputs:**
- `imageURL` (string, required): URL of the image to remove background from
- `max_retries` (number, optional): Maximum number of polling attempts (default: 30)
- `retry_interval` (number, optional): Interval between polling attempts in seconds (default: 2)

**Outputs:**
- `result_url` (string): URL of the processed image with background removed

**Use Case:** Perfect for processing web-hosted images or when you want to keep images in the cloud.

### 2. File Image Background Removal

Remove background from a local image file and save the processed result.

**Inputs:**
- `image_file` (file, required): Local image file to process
- `saved_path` (string, optional): Path to save the processed image
- `max_retries` (number, optional): Maximum number of polling attempts (default: 30)
- `retry_interval` (number, optional): Interval between polling attempts in seconds (default: 2)

**Outputs:**
- `saved_path` (string): Path of the successfully downloaded processed image

**Use Case:** Ideal for batch processing local images or integrating background removal into file-based workflows.

## Basic Usage

### Using URL Image Background Removal

1. Add the `url-image-background-removal` subflow to your workflow
2. Connect an image URL to the `imageURL` input
3. The processed image URL will be available in the `result_url` output

### Using File Image Background Removal

1. Add the `file-image-background-removal` subflow to your workflow
2. Select a local image file using the `image_file` input
3. Optionally specify where to save the result in `saved_path`
4. The processed image will be saved and its path returned in the output

## Task Blocks

This package includes two core task blocks (marked as private for internal use):

### Submit Background Removal

Submits an image to the background removal API and returns a request ID for tracking the job status.

### Get Background Removal Result

Polls the background removal API to retrieve the processed image URL once the job is complete.

## Dependencies

This package requires the following OOMOL packages:
- `upload-to-cloud` (v0.0.5): For uploading local files to cloud storage
- `downloader` (v0.1.1): For downloading processed images

## Installation

This package can be installed through the OOMOL package manager:

```bash
# Install the package
oomol install bria-removebg

# Add to your workspace dependencies
oomol use bria-removebg
```

## Configuration

The background removal service uses the OOMOL Fusion API. No additional API key configuration is required - the package automatically uses your OOMOL token for authentication.

## Technical Details

### Workflow Architecture

Both subflows follow a similar pattern:

1. **Submit Phase**: Submit the image (URL or uploaded file) to the BRIA API
2. **Poll Phase**: Continuously check the job status until completion
3. **Retrieve Phase**: Return or download the processed image

### Polling Mechanism

The polling system includes:
- Configurable retry attempts to handle long processing times
- Adjustable retry intervals to balance responsiveness and API load
- Automatic error handling and status reporting

### API Integration

The package integrates with the BRIA AI background removal API through OOMOL's Fusion API endpoint:
- Base URL: `https://fusion-api.oomol.com/v1`
- Authentication: Automatic via OOMOL token
- Endpoints: `/image/background-removal` for submission and result retrieval

## Error Handling

The package includes robust error handling:
- Connection failures are reported with clear error messages
- Timeout scenarios are handled gracefully
- Job status is tracked and reported throughout the process

## Version

Current version: 0.0.1

## License

This package is provided as part of the OOMOL ecosystem.
