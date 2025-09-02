import SwiftUI
import AVKit

struct Subtitle: Codable {
    let text: String
    let start: Double
    let end: Double
}

struct SyncedSubtitleView: View {
    let videoURL: URL
    let subtitles: [Subtitle]
    @State private var currentText = ""
    @State private var player = AVPlayer()

    var body: some View {
        VStack {
            VideoPlayer(player: player)
                .frame(height: 300)
                .onAppear {
                    player.replaceCurrentItem(with: AVPlayerItem(url: videoURL))
                    player.play()
                    startSync()
                }

            Text(currentText)
                .font(.title2)
                .padding()
        }
    }

    func startSync() {
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            let currentTime = player.currentTime().seconds
            if let match = subtitles.first(where: { currentTime >= $0.start && currentTime <= $0.end }) {
                currentText = match.text
            }
        }
    }
}
