namespace ActiveRecoveryAssist.Presentation;
public partial class AskViewModel : ObservableObject
{
    private INavigator _navigator;

    public AskViewModel(
        IStringLocalizer localizer,
        IOptions<AppConfig> appInfo,
        INavigator navigator)
    {
        _navigator = navigator;
    }
}
