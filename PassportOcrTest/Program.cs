using System.Text.Json;
using RapidOcrNet;

string baseDir = AppContext.BaseDirectory;
var modelSet = RapidOcrModelSet.PPOCRv6Small with
{
    DetModelPath = Path.Combine(baseDir, "models", "v6", "PP-OCRv6_det_small.onnx"),
    ClsModelPath = Path.Combine(baseDir, "models", "v5", "ch_PP-LCNet_x0_25_textline_ori_cls_mobile.onnx"),
    RecModelPath = Path.Combine(baseDir, "models", "v6", "PP-OCRv6_rec_small.onnx"),
    KeysPath     = Path.Combine(baseDir, "models", "v6", "ppocrv6_small_dict.txt")
};

using var ocr = new RapidOcr();
ocr.InitModels(modelSet);

string testDir = Path.GetFullPath(args.Length > 0 ? args[0] : "test-passport");
var files = Directory.GetFiles(testDir, "*.*")
    .Where(f => f.EndsWith(".jpg", StringComparison.OrdinalIgnoreCase) ||
                f.EndsWith(".jpeg", StringComparison.OrdinalIgnoreCase) ||
                f.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
    .OrderBy(f => Path.GetFileName(f))
    .ToList();

Console.WriteLine($"Found {files.Count} images in {testDir}");

var allResults = new Dictionary<string, object>();

foreach (var file in files)
{
    string fileName = Path.GetFileName(file);
    try
    {
        var sw = System.Diagnostics.Stopwatch.StartNew();
        OcrResult result = ocr.Detect(file, RapidOcrOptions.PPOCRv6);
        sw.Stop();

        var blocks = new List<object>();
        if (result.TextBlocks != null)
        {
            foreach (var b in result.TextBlocks)
            {
                blocks.Add(new
                {
                    Text = b.Text,
                    Score = b.BoxScore,
                    CharAvg = b.CharScores?.Length > 0 ? b.CharScores.Average() : 0f,
                    Points = b.BoxPoints.Select(p => new[] { p.X, p.Y }).ToArray()
                });
            }
        }

        allResults[fileName] = new
        {
            TimeMs = sw.ElapsedMilliseconds,
            DetectTime = result.DetectTime,
            DbNetTime = result.DbNetTime,
            Blocks = blocks,
            FullText = result.StrRes
        };
        Console.WriteLine($"[C#] {fileName}: {sw.ElapsedMilliseconds} ms, {blocks.Count} text blocks");
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine($"[C# Error] {fileName}: {ex.Message}");
        allResults[fileName] = new { Error = ex.Message };
    }
}

string json = JsonSerializer.Serialize(allResults, new JsonSerializerOptions { WriteIndented = true });
string outPath = Path.Combine(Directory.GetCurrentDirectory(), "csharp_test_passport_benchmark.json");
File.WriteAllText(outPath, json);
Console.WriteLine($"C# benchmark completed. Saved {allResults.Count} results to {outPath}");
