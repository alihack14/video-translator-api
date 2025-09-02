static func fetchSyncedSubtitles(videoURL: URL, targetLang: String, completion: @escaping ([Subtitle]) -> Void) {
    // نفس إعدادات request السابقة
    // بعد استلام البيانات:
    let decoder = JSONDecoder()
    if let subtitles = try? decoder.decode([Subtitle].self, from: data) {
        DispatchQueue.main.async {
            completion(subtitles)
        }
    }
}
