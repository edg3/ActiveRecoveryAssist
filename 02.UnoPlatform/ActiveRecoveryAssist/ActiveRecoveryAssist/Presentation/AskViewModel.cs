using ActiveRecoveryAssist.Services.Azure;

namespace ActiveRecoveryAssist.Presentation;
public partial class AskViewModel : ObservableObject
{
    private INavigator _navigator;

    [ObservableProperty]
    private string question = string.Empty;

    public AskViewModel(
        IStringLocalizer localizer,
        IOptions<AppConfig> appInfo,
        INavigator navigator)
    {
        _navigator = navigator;

        Ask = new RelayCommand(async () => await AskCommand());
    }

    public ICommand Ask { get; }

    private async Task AskCommand()
    {
        // Add the question to the database
        ADB.Add(new Question { Text = Question });
        ADB.Save();

        // Navigate back to the main page
        await _navigator.GoBack(this);
    }
}
