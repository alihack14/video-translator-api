import SwiftUI
import PhotosUI
import AVKit

struct VideoPickerView: View {
    @State private var selectedItem: PhotosPickerItem? = nil
    @State private var videoURL: URL? = nil
    @State private var isUploading = false
    @State private var uploadStatus = ""
    @State private var translatedText = ""
    @State private var selectedLanguage = "ar"
    @State private var syncedSubtitles: [Subtitle] = []
    @State private var showSyncedView = false

    let supportedLanguages = ["ar", "en", "fr", "es", "de", "zh"]

    var body: some View {
        VStack(spacing: 20) {
            Picker("اختر اللغة", selection: $selectedLanguage) {
                ForEach(supportedLanguages, id: \.self) { lang in
                    Text(lang.uppercased())
                }
            }
            .pickerStyle(SegmentedPickerStyle())

            PhotosPicker(selection: $selectedItem, matching: .videos) {
                Text("اختر فيديو من جهازك")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }

            if let url = videoURL {
                Text("تم اختيار: \(url.lastPathComponent)")
                Button("ترجم الفيديو") {
                    isUploading = true
                    translatedText = ""
                    APIService.uploadVideoWithTranslation(videoURL: url, targetLang: selectedLanguage) { chunk in
                        translatedText += chunk + "
"
                    } completion: { success in
                        isUploading = false
                        uploadStatus = success ? "تم التحميل بنجاح" : "فشل في التحميل"
                    }
                }

                Button("عرض الترجمة المتزامنة") {
                    APIService.fetchSyncedSubtitles(videoURL: url, targetLang: selectedLanguage) { subtitles in
                        syncedSubtitles = subtitles
                        showSyncedView = true
                    }
                }

                SyncedSubtitlePlayerView(videoURL: url, subtitles: syncedSubtitles)
                    .frame(height: 300)

                Button("تشغيل خارجي مع الترجمة") {
                    ExternalPlayerHelper.launchExternalPlayer(videoURL: url, subtitles: syncedSubtitles)
                }
            }

            if isUploading {
                ProgressView("جاري التحميل...")
            }

            Text(uploadStatus)

            if !translatedText.isEmpty {
                Text("الترجمة:")
                    .font(.headline)
                ScrollView {
                    Text(translatedText)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(10)
                }
            }

            NavigationLink("مشاهدة الترجمة المتزامنة", isActive: $showSyncedView) {
                SyncedSubtitleView(videoURL: videoURL!, subtitles: syncedSubtitles)
            }
        }
        .padding()
        .onChange(of: selectedItem) { newItem in
            Task {
                if let data = try? await newItem?.loadTransferable(type: Data.self),
                   let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("selectedVideo.mp4") {
                    try? data.write(to: tempURL)
                    videoURL = tempURL
                }
            }
        }
    }
}