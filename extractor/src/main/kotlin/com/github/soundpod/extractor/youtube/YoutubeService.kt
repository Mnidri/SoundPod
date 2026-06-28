package com.github.musick.extractor.youtube

class YoutubeService {
    fun getStreamExtractor(url: String): YoutubeStreamExtractor {
        return YoutubeStreamExtractor(url)
    }
}
