using ActiveRecoveryAssist.Services.Azure;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

namespace ActiveRecoveryAssist.Models;
public class Question : Model
{
    public int QuestionID { get; set; }
    public string Device { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public string? Answer { get; set; }

    // TODO: get device serial (or something) for uniqueness
    // TODO: this might not be needed at all, was just an issue with my complex data types before
    public override void Insert()
    {
        var strQuery = "INSERT INTO Question (Device, Text, Answer) VALUES (@Device, @Text, @Answer);";
        using var cmd = ADB.AzureDb!.Database.GetDbConnection().CreateCommand();
        cmd.CommandText = strQuery;
        cmd.Parameters.Add(new SqlParameter("@Device", "device1"));
        cmd.Parameters.Add(new SqlParameter("@Text", Text));
        cmd.Parameters.Add(new SqlParameter("@Answer", Answer));

        if (cmd.Connection is null) throw new Exception();
        cmd.Connection.Open();
        cmd.ExecuteNonQuery();
        cmd.Connection.Close();
    }

    public override void Update()
    {
        var strQuery = "UPDATE Question SET Device = @Device, Text = @Text, Answer = @Answer WHERE QuestionID = @QuestionID;";
        using var cmd = ADB.AzureDb!.Database.GetDbConnection().CreateCommand();
        cmd.CommandText = strQuery;
        cmd.Parameters.Add(new SqlParameter("@QuestionID", QuestionID));
        cmd.Parameters.Add(new SqlParameter("@Device", "device1"));
        cmd.Parameters.Add(new SqlParameter("@Text", Text));
        cmd.Parameters.Add(new SqlParameter("@Answer", Answer));

        if (cmd.Connection is null) throw new Exception();
        cmd.Connection.Open();
        cmd.ExecuteNonQuery();
        cmd.Connection.Close();
    }
}
