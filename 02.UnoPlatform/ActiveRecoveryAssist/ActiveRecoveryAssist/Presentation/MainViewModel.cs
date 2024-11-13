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
    }

    //public ICommand GoToAdd<name> { get; } // get; is important

    //private async Task GoTo<name>() // This is using the code in App.xaml.cs function "RegisterRoutes"
    //{
    //    await _navigator.NavigateViewModelAsync<<name>ViewModel>(this);
    //}
}
