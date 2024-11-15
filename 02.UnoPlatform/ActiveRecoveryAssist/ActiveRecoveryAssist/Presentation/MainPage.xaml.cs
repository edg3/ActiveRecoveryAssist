namespace ActiveRecoveryAssist.Presentation;

public sealed partial class MainPage : Page
{
    public MainPage()
    {
        this.InitializeComponent();
    }

    private void Button_Click(object sender, RoutedEventArgs e)
    {
        lstBroken.ItemsSource = MainViewModel.I!.Questions;
    }
}
