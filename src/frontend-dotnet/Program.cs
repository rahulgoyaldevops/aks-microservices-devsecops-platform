var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient("BackendClient", client =>
{
    var backendUrl = builder.Configuration["BACKEND_API_URL"] ?? "http://backend-python:8000";
    client.BaseAddress = new Uri(backendUrl);
    client.Timeout = TimeSpan.FromSeconds(5);
});

var app = builder.Build();

app.MapGet("/", async (IHttpClientFactory httpClientFactory, IConfiguration config) =>
{
    var backendUrl = config["BACKEND_API_URL"] ?? "http://backend-python:8000";
    try
    {
        var client = httpClientFactory.CreateClient("BackendClient");
        var response = await client.GetAsync("/api/v1/status");
        var content = await response.Content.ReadAsStringAsync();
        return Results.Ok(new
        {
            service = "frontend-dotnet",
            backendUrl,
            backendStatus = (int)response.StatusCode,
            backendResponse = content
        });
    }
    catch (Exception ex)
    {
        return Results.Ok(new
        {
            service = "frontend-dotnet",
            backendUrl,
            backendStatus = "unreachable",
            error = ex.Message
        });
    }
});

app.MapGet("/healthz", () => Results.Ok(new { status = "healthy" }));

app.MapGet("/readyz", () => Results.Ok(new { status = "ready" }));

app.Run();
