#!/bin/bash
# Regenera el README, hace commit y push. Uso: scripts/publicar.sh "mensaje"
set -e
cd "$(dirname "$0")"
python3 readme.py
python3 pagina_cuadernos.py
python3 presentaciones.py
cd ..
git add -A
git -c user.name="Fernando Borrás Rocher" -c user.email="f.borras@umh.es" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01BtDJKkMPUBqoxamnhxNApf"
git -c push.negotiate=true push -q origin main 2>&1 | grep -iv negotiat || true
echo "local $(git rev-parse --short HEAD) · remoto $(git ls-remote origin main | cut -c1-7)"
