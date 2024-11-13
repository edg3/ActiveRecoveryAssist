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