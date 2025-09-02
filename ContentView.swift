import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("مترجم الفيديو الذكي")
                    .font(.title)
                    .bold()

                NavigationLink("اختر فيديو", destination: VideoPickerView())
                NavigationLink("الفيديوهات المترجمة", destination: TranslatedListView())
            }
            .padding()
        }
    }
}