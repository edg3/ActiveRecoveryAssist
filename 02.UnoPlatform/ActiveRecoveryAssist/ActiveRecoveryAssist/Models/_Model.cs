using ActiveRecoveryAssist.Services.Azure;

namespace ActiveRecoveryAssist.Models;

/// <summary>
/// Use Raw SQL to insert/update data in the Azure SQL database.
///  - This was only needed since my old hardware has slight troubles saving inserts/updates to the database, for some reason.
/// </summary>
public abstract class Model
{
    /// <summary>
    /// Action that inserts the model to the DB
    /// </summary>
    public abstract void Insert();
    /// <summary>
    /// Action that uses updates the model in the FB
    /// </summary>
    public abstract void Update();
}
