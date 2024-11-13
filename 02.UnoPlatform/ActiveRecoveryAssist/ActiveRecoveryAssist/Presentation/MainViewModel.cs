using System.Collections.ObjectModel;
using ActiveRecoveryAssist.Services.Azure;

namespace ActiveRecoveryAssist.Presentation;

public partial class MainViewModel : ObservableObject
{
    private INavigator _navigator;

    AzureDb azureDb;

    public MainViewModel(
        IStringLocalizer localizer,
        IOptions<AppConfig> appInfo,
        INavigator navigator)
    {
        _navigator = navigator;

        azureDb = new AzureDb();

        GoAsk = new RelayCommand(async () => await GoAskCommand());
    }

    public ICommand GoAsk { get; }

    private async Task GoAskCommand()
    {
        await _navigator.NavigateViewModelAsync<AskViewModel>(this);
    }
}
