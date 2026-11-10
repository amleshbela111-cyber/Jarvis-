# Jarvis (community)

Jarvis is an Android voice assistant. It listens to voice commands, answers with Gemini, and can help control the phone with the user's permission.

## Using it
- The app needs your own Gemini API key, entered in the app. Keys are stored only on your phone.
- Device-control features need permissions you grant yourself.

## Building
1. Open the `JarvisAI` folder in Android Studio, or build with `./gradlew assembleDebug`.
2. Minimum Android version: 8.0 (API 26). Build target: API 35.

## Contributing
Read CONTRIBUTING.md and SECURITY.md first.

## Checking a change yourself
```
python3 tools/scan_patch.py <original_folder> <changed_folder> report.md
```
The report lists new network addresses, permissions, secret-looking strings and risky calls. Exit code 2 means a person must review it.

## License
Add your chosen license here before publishing.
