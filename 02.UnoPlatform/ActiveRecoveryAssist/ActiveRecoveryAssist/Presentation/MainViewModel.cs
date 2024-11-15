using System.Collections.ObjectModel;
using ActiveRecoveryAssist.Services.Azure;

namespace ActiveRecoveryAssist.Presentation;

/// <summary>
/// Notes:
///  - Copilot use: I always use inline (with the question keyboard shortcuts), which never shows as 'using copilot' - was a flaw for the hackathon review. It appeared I don't (after using for years)
/// </summary>
public partial class MainViewModel : ObservableObject
{
    internal static MainViewModel? I { get; set; }

    private INavigator _navigator;

    AzureDb azureDb;
    Thread _refreshThread;

    [ObservableProperty]
    ObservableCollection<string> questions = new();

    public MainViewModel(
        IStringLocalizer localizer,
        IOptions<AppConfig> appInfo,
        INavigator navigator)
    {
        _navigator = navigator;
        I = this;

        azureDb = new AzureDb();

        GoAsk = new RelayCommand(async () => await GoAskCommand());
        GetQuestions();
    }

    public async void GetQuestions()
    {
        // TODO: think this one through
        Questions.Clear();
        var qns = ADB.Questions.Where(it => true)
            .OrderByDescending(it => it.QuestionID)
            .ToList();
        qns.ForEach(it =>
        {
            if (it.Answer is null || it.Answer.Length < 1)
            {
                Questions.Add("Awaiting Response: " + it.Text);
            }
            else
            {
                Questions.Add("[Remember this answer comes from an ML model and may not be correct, proceed with caution] " + it.Answer);
            }
        });
    }

    public ICommand GoAsk { get; }

    private async Task GoAskCommand()
    {
        await _navigator.NavigateViewModelAsync<AskViewModel>(this);
    }

    // TODO: update list after you ask a question
}
