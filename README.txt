JARVIS ENERGY CORE — GITHUB ACTIONS BUILD + TERMUX PUSH

BUILD FILE
The requested GitHub Actions workflow is:
.github/workflows/build.yml

GitHub only automatically detects Actions workflow files when they are placed
inside .github/workflows/. The file is named build.yml (YAML), not build.xml.

WHAT THE WORKFLOW DOES
- Runs automatically on pushes and pull requests targeting main.
- Can also be started manually with Actions > Build JARVIS Energy Core > Run workflow.
- Checks required PWA files and validates manifest JSON, service worker references,
  and PNG icon signatures.
- Creates dist/Jarvis-AI-PWA.zip.
- Uploads the ZIP as a downloadable Actions artifact named Jarvis-AI-PWA.

TERMUX SETUP
pkg update && pkg upgrade
pkg install git gh

Log in to GitHub once:
gh auth login

Extract the ZIP, enter the project folder, then run:
chmod +x push-to-github.sh
./push-to-github.sh

The script creates a PRIVATE repository named Jarvis-AI under the GitHub account
authenticated with `gh`, if it does not already exist, and pushes the project.
After a successful push, GitHub Actions starts the build workflow automatically.

Optional repository name and branch:
./push-to-github.sh Jarvis-AI main

HOW TO DOWNLOAD THE BUILT ZIP
Open the repository on GitHub > Actions > latest successful
"Build JARVIS Energy Core" run > Artifacts > Jarvis-AI-PWA.

PWA INSTALLATION
For Chrome installation, deploy the contents of the artifact to an HTTPS host.
Opening index.html directly from local Downloads (file://) does not enable PWA
installation. Chrome installation requires HTTPS (or localhost).

IMPORTANT LIMITATIONS
This is a Three.js web/PWA project. build.yml creates and validates a web app
bundle; it does not generate an APK. A native APK requires a separate Android
project (for example, a Capacitor/Android or native Gradle wrapper).

The Three.js modules are imported from jsDelivr. The first launch needs internet;
the service worker caches the app shell, but external 3D modules are not bundled.
