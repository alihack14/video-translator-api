import Foundation
import UIKit

struct ExternalPlayerHelper {
    static func launchExternalPlayer(videoURL: URL, subtitles: [Subtitle]) {
        let srtText = subtitles.enumerated().map { (i, sub) in
            let start = formatTimestamp(sub.start)
            let end = formatTimestamp(sub.end)
            return "\(i+1)
\(start) --> \(end)
\(sub.text)"
        }.joined(separator: "

")

        let srtPath = FileManager.default.temporaryDirectory.appendingPathComponent("subtitles.srt")
        try? srtText.write(to: srtPath, atomically: true, encoding: .utf8)

        let controller = UIDocumentInteractionController(url: videoURL)
        controller.uti = "public.movie"
        DispatchQueue.main.async {
            if let root = UIApplication.shared.windows.first?.rootViewController {
                controller.presentOpenInMenu(from: root.view.frame, in: root.view, animated: true)
            }
        }
    }

    static func formatTimestamp(_ seconds: Double) -> String {
        let hrs = Int(seconds / 3600)
        let mins = Int((seconds.truncatingRemainder(dividingBy: 3600)) / 60)
        let secs = Int(seconds.truncatingRemainder(dividingBy: 60))
        let millis = Int((seconds - Double(Int(seconds))) * 1000)
        return String(format: "%02d:%02d:%02d,%03d", hrs, mins, secs, millis)
    }
}