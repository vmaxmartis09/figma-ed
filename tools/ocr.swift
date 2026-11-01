import Foundation
import Vision
import AppKit
// usage: ocr <image> ...   prints JSON {path: [{text, x, y, w, h}]} in source pixels
var out: [String: Any] = [:]
for p in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: p), var cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let scale = 3
    let w = cg.width * scale, h = cg.height * scale
    if let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) {
        ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1)); ctx.fill(CGRect(x: 0, y: 0, width: w, height: h))
        ctx.interpolationQuality = .high; ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
        if let big = ctx.makeImage() { cg = big }
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.automaticallyDetectsLanguage = true
    let hnd = VNImageRequestHandler(cgImage: cg, options: [:])
    try? hnd.perform([req])
    var lines: [[String: Any]] = []
    for o in req.results ?? [] {
        guard let t = o.topCandidates(1).first else { continue }
        let b = o.boundingBox
        lines.append(["text": t.string, "x": b.minX * Double(cg.width) / Double(scale), "y": (1 - b.maxY) * Double(cg.height) / Double(scale), "w": b.width * Double(cg.width) / Double(scale), "h": b.height * Double(cg.height) / Double(scale), "conf": t.confidence])
    }
    out[p] = lines
}
let d = try! JSONSerialization.data(withJSONObject: out, options: [.prettyPrinted])
print(String(data: d, encoding: .utf8)!)
