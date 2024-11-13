namespace ActiveRecoveryAssist.Models;

public record AppConfig
{
    public string? Environment { get; init; }
    internal static string DbPass { get; } = "password";
}
