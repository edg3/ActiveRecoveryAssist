using System.Collections.ObjectModel;
using ActiveRecoveryAssist.Services.Azure;

namespace ActiveRecoveryAssist.Presentation;

public partial class MainViewModel : ObservableObject
{
    private INavigator _navigator;

    AzureDb azureDb;

    [ObservableProperty]
    List<Question> questions = new();

    public MainViewModel(
        IStringLocalizer localizer,
        IOptions<AppConfig> appInfo,
        INavigator navigator)
    {
        _navigator = navigator;

        azureDb = new AzureDb();

        GoAsk = new RelayCommand(async () => await GoAskCommand());
        GetQuestions();
    }

    public async void GetQuestions()
    {
        // TODO: think this one through
        var qns = ADB.Questions.Where(it => true).ToList();
        Questions.AddRange(qns);
    }

    public ICommand GoAsk { get; }

    private async Task GoAskCommand()
    {
        await _navigator.NavigateViewModelAsync<AskViewModel>(this);
    }

    // TODO: update list after you ask a question
}
