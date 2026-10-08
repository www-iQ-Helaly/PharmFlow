#!/usr/bin/env bash
# Build the site locally and upload it to your VPS. Run from the project root.
#
#   SITE_URL=https://pharmflow.example.com \
#   VPS_HOST=203.0.113.10 VPS_USER=deploy VPS_PATH=/var/www/pharmflow \
#   ./deploy/deploy.sh
#
# Authentication uses your normal SSH key/agent. No credentials are stored here.
set -euo pipefail

: "${SITE_URL:?set SITE_URL, e.g. https://pharmflow.example.com}"
: "${VPS_HOST:?set VPS_HOST}"
: "${VPS_USER:?set VPS_USER}"
VPS_PATH="${VPS_PATH:-/var/www/pharmflow}"

npm ci
npm run check
SITE_URL="$SITE_URL" npm run build

# --delete keeps the server identical to dist/. Remove it if you add files by hand.
rsync -az --delete dist/ "${VPS_USER}@${VPS_HOST}:${VPS_PATH}/"

echo "Deployed to ${SITE_URL}"
