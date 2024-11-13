using ActiveRecoveryAssist.Services.Azure;

namespace ActiveRecoveryAssist.Models;

/// <summary>
/// Use Raw SQL to insert/update data in the Azure SQL database.
///  - This was only needed since my old hardware has slight troubles saving inserts/updates to the database, for some reason.
/// </summary>
public abstract class Model
{
    /// <summary>
    /// Get the Insert SQL query text
    /// </summary>
    /// <returns>@parameterised SQL string</returns>
    public abstract string InsertSQL();
    /// <summary>
    /// Action that uses InsertSQL to get the @parameters string, then adds the parameters and executes the command with ExecuteNonQuery().
    /// </summary>
    public abstract void Insert();
    /// <summary>
    /// Get the Update SQL query text
    /// </summary>
    /// <returns>@parameterised SQL string</returns>
    public abstract string UpdateSQL();
    /// <summary>
    /// Action that uses UpdateSQL to get the @parameters string, then adds the parameters and executes the command with ExecuteNonQuery().
    /// </summary>
    public abstract void Update();
}
