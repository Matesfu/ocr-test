
using RapidOCRLib;

if (args.Length != 1)
{
    Console.Error.WriteLine("Usage: dotnet run -- <passport-image-path>");
    return;
}

string passportPath = Path.GetFullPath(args[0]);
if (!File.Exists(passportPath))
{
    Console.Error.WriteLine($"Image file not found: {passportPath}");
    return;
}

string modelsPath = Path.Combine(AppContext.BaseDirectory, "models");
OcrLite ocr = new()
{
    DetPath = Path.Combine(modelsPath, "ch_PP-OCRv5_mobile_det.onnx"),
    ClsPath = Path.Combine(modelsPath, "ch_ppocr_mobile_v2.0_cls_infer.onnx"),
    RecPath = Path.Combine(modelsPath, "ch_PP-OCRv5_rec_mobile_infer.onnx"),
    KeyDicPath = Path.Combine(modelsPath, "ppocrv5_dict.txt"),
};

string[] lines;
TextWriter standardOutput = Console.Out;
Console.SetOut(TextWriter.Null);

try
{
    await ocr.InitModels();
    var result = ocr.Detect(passportPath, padding: 50);
    if (result is null)
    {
        Console.Error.WriteLine("OCR did not return a result.");
        return;
    }

    lines = result.StrRes.Split(
        new[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries);
}
finally
{
    Console.SetOut(standardOutput);
}

if (lines.Length < 2)
{
    Console.Error.WriteLine("OCR returned fewer than two text lines.");
    return;
}

Console.WriteLine(lines[^2]);
Console.WriteLine(lines[^1]);
