static let serverURL = "https://video-translator-api-5.onrender.com"
    // نفس إعدادات request السابقة
    // بعد استلام البيانات:
    let decoder = JSONDecoder()
    if let subtitles = try? decoder.decode([Subtitle].self, from: data) {
        DispatchQueue.main.async {
            completion(subtitles)
        }
    }
}
body.append("--\(boundary)\r\n".data(using: .utf8)!)
body.append("Content-Disposition: form-data; name=\"format\"\r\n\r\n".data(using: .utf8)!)
body.append("json\r\n".data(using: .utf8)!)
