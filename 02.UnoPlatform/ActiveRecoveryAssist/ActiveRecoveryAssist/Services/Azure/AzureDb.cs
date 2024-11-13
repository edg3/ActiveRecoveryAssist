using Microsoft.EntityFrameworkCore;

namespace ActiveRecoveryAssist.Services.Azure;

internal static class ADB
{
    public static AzureDb? AzureDb { get; internal set; } = null;

    public static void Add(object obj) => AzureDb!.Add(obj);
    public static void Save() => AzureDb!.SaveChanges();
}

internal class AzureDb : DbContext
{
    public AzureDb()
    {
        if (ADB.AzureDb == null)
        {
            ADB.AzureDb = this;
        }
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer($"Server=tcp:edg3.database.windows.net,1433;Initial Catalog=NaNoEDb;Persist Security Info=False;User ID=edg3;Password=\"{AppConfig.DbPass}\";MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=60;MultipleActiveResultSets=True");
    }

    //public DbSet<<name>> <name> { get; set; } // This adds the DB set for the named model

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // This sets up the proper interaction
        //modelBuilder.Entity<<name>>().ToTable("<name>");
        //modelBuilder.Entity<<name>>().HasKey(n => n.<nameof>ID);
    }
}
