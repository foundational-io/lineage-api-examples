#!/bin/bash

# Set the image name
image_name="hello-lineage-graph-example"

# Build the Docker image
docker buildx build -t "$image_name" .

# Run the tests in the Docker container
docker run "$image_name"