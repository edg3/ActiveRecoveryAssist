# ActiveRecoveryAssist

## Logic

This will start off as a simple app for Alpha-1 (Android) that connects to my Azure DB for simple 'questions and answers' first that go to my slightly adjusted query answer model using '01.ML-model' on my home machine to answer questions.

## Alpha-1

*Note: Do as much auto code creation using copilot for hackathon so Alpha-1 => copilot code*

- Connect to Azure DB - unique phone identifier to link to messages
- Ask question - If message is safe text, it can ask the model (i.e. will state 'please dont use offensive language', will be for super safety, so can't even use 'pleasure' questions, this may need super testing)
- Asked question logs in Azure DB as 'unanswered'
- View to pop back to each message you sent, and search filter to find them again (shows unanswered if it hasn't gone to model yet)
- Shows answered if model gave answer (i.e. start final version of *01.ML-model* using Azure)

## Notes:

### 0. Pro Tips

- Alt+/ - use copilot in VS2022
- VSCode - rather use Ctrl+I
- On older hardware, it might not give error Hyper-V not enabled, but will run once in a while. Check in Windows Features - https://learn.microsoft.com/en-us/dotnet/maui/android/emulator/hardware-acceleration?view=net-maui-8.0 - tick all Hyper-V options shown in URL; there are alternatives if you need, though
- Promote: Pen to paper policy!! To achieve ANYTHING
- If emulator launched and still gets stuck on VS2022 showing it hasnt finished launching: Android Device Manager -> Factory Reset emu
- 
### 1. AppConfig.cs

If you need to have a base file with something like '<insert azure password here>' as a string, set it to skip work tree:

- git update-index --skip-worktree AppConfig.cs

That will make it ignore changes to file; when we need to add changes, make sure auth secure string is taken away and do the following to commit the extra you needed, then skip worktree again and put the password back. NEVER share passwords in code ANYWHERE.

- git update-index --no-skip-worktree AppConfig.cs

### 2. Compile APK

- dotnet publish -f net8.0-android -c Release -o ./publish

OR (if above doesn't work)

- in VS2022, in the sln folder:
    keytool -genkeypair -v -keystore key.keystore -alias key -keyalg RSA -keysize 2048 -validity 10000
- see list
    keytool -list -keystore key.keystore
- publish APK, in vs powershell, in folder of sln & key:
    dotnet publish -f net8.0-android -c Release -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=../key.keystore -p:AndroidSigningKeyAlias=key -p:AndroidSigningKeyPass=edg3za -p:AndroidSigningStorePass=edg3za
- bin\Release\net8.0-android\publish