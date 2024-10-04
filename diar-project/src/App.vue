<template>
  <div id="app">
    <video-player
        :videoSrc="videoSrc"
        @setPlaybackRate="setPlaybackRate"
        ref="videoPlayer"
        @timeupdate="onVideoTimeUpdate"
      ></video-player>
    <transcription
      :transcript="transcript"
      :speakers="speakers"
      :currentTime="currentTime"
      @selectWord="selectWord"
      @assignSpeaker="assignSpeaker"
    ></transcription>
    <speaker-list
        :speakers="speakers"
        @addSpeaker="addSpeaker"
        @removeSpeaker="removeSpeaker"
        @updateSpeakerName="updateSpeakerName"
      ></speaker-list>
    <hotkeys-info></hotkeys-info>
  </div>
</template>

<script>
import VideoPlayer from './components/VideoPlayer.vue';
import SpeakerList from './components/SpeakerList.vue';
import Transcription from './components/Transcription.vue';
import HotkeysInfo from './components/HotkeysInfo.vue';

export default {
  name: 'App',
  components: {
    VideoPlayer,
    SpeakerList,
    Transcription,
    HotkeysInfo
  },
  data() {
    return {
      videoSrc: '',
      file_id:'file_id',
      speakers: [
        { id: 'Speaker_1', name: 'Спикер 1', color: '#FF5733' },
        { id: 'Speaker_2', name: 'Спикер 2', color: '#33C1FF' }
      ],
      transcript: [],
      selectedWord: null,
      currentTime: 0,
    };
  },
  mounted() {
    // Загрузить расшифровку из JSON-файла
    fetch('/task')
      .then(response => response.json())
      .then(data => {
        this.transcript = data["text"];
        this.videoSrc = data["video"];
        this.file_id = data["file_id"]
      });

    // Обработка горячих клавиш
    window.addEventListener('keydown', this.handleHotkeys);
  },
  methods: {
    setPlaybackRate(rate) {
      this.$refs.videoPlayer.setPlaybackRate(rate);
    },
    addSpeaker() {
      if (this.speakers.length < 9) {
        const newId = `Speaker_${this.speakers.length + 1}`;
        const newColor = '#' + Math.floor(Math.random() * 16777215).toString(16);
        this.speakers.push({ id: newId, name: newId, color: newColor });
      }
    },
    removeSpeaker(speakerId) {
      this.speakers = this.speakers.filter(s => s.id !== speakerId);
    },
    updateSpeakerName(speakerId, newName) {
      const speaker = this.speakers.find(s => s.id === speakerId);
      if (speaker) speaker.name = newName;
    },
    selectWord(word) {
      this.selectedWord = word;
      this.$refs.videoPlayer.seekTo(word.start);
    },
    assignSpeaker(speakerId) {
    if (this.selectedWord) {
      const originalSpeakerId = this.selectedWord.speakerId || null;
      let found = false;
      for (let sentence of this.transcript) {
        for (let word of sentence.words) {
          if (word === this.selectedWord) {
            found = true;
            word.speakerId = speakerId;
            continue;
          }
          if (found) {
            if (originalSpeakerId !== null && word.speakerId !== originalSpeakerId) {
              // Встретили слово с другим спикером, прекращаем изменение
              break;
            }
            word.speakerId = speakerId;
          }
        }
        if (found) {
          // Если изменение завершено внутри предложения, прекращаем цикл
          break;
        }
      }
      this.exportResults();
      this.selectedWord = null; // Сброс выбранного слова
    }
  },
    handleHotkeys(event) {
      if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return; // Не обрабатывать горячие клавиши в полях ввода
      }
      if (event.key === ' ') {
        event.preventDefault();
        this.$refs.videoPlayer.playPause();
      } else if (event.key >= '1' && event.key <= '9') {
        const index = parseInt(event.key) - 1;
        if (this.speakers[index]) {
          this.assignSpeaker(this.speakers[index].id);
        }
      } else if (event.key === '0') {
        this.assignSpeaker(null);
      } else if (event.key === '+') {
        this.$refs.videoPlayer.increasePlaybackRate();
      } else if (event.key === '-') {
        this.$refs.videoPlayer.decreasePlaybackRate();
      }
    },
    onVideoTimeUpdate(time) {
      this.currentTime = time;
    },
    exportResults() {
      const result = [];
      for (let sentence of this.transcript) {
        for (let word of sentence.words) {
          result.push({
            word: word.word,
            speakerId: word.speakerId || null
          });
        }
      }
      // Отправка на сервер
      fetch('/result', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"file_id": this.file_id, "data":result})
      });
    }
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleHotkeys);
  }
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 20px;
}
.top-section {
  display: flex;
  justify-content: space-between;
}
</style>
