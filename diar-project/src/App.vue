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
      @seekTo="seekToTime"
    ></transcription>
    <speaker-list
        :speakers="speakers"
        @addSpeaker="addSpeaker"
        @removeSpeaker="removeSpeaker"
        @updateSpeakerName="updateSpeakerName"
      ></speaker-list>
    <hotkeys-info></hotkeys-info>
    <save-result @save-and-reload="saveAndReload"></save-result>
  </div>
</template>

<script>
import VideoPlayer from './components/VideoPlayer.vue';
import SpeakerList from './components/SpeakerList.vue';
import Transcription from './components/Transcription.vue';
import HotkeysInfo from './components/HotkeysInfo.vue';
import SaveResult from './components/SaveResult.vue';

export default {
  name: 'App',
  components: {
    VideoPlayer,
    SpeakerList,
    Transcription,
    HotkeysInfo,
    SaveResult
  },
  data() {
    return {
      videoSrc: '',
      file_id:'file_id',
      speakers: [],
      transcript: [],
      selectedWord: null,
      currentTime: 0,
      channel:'',
    };
  },
  mounted() {
    // Загрузить расшифровку из JSON-файла
    fetch('/api/task')
      .then(response => {
        if (response.status === 404) {
          alert('Задачи закончились');
          return;
        }
        return response.json();
      })
      .then(data => {
        if (data) {
          this.transcript = data["text"];
          this.videoSrc = data["video"];
          this.file_id = data["file_id"]
          this.speakers = data["speakers"]
          this.channel = data["channel_id"]
        }
      });

    // Обработка горячих клавиш
    window.addEventListener('keydown', this.handleHotkeys);
  },
  methods: {
    setPlaybackRate(rate) {
      this.$refs.videoPlayer.setPlaybackRate(rate);
    },
    addSpeaker() {
      if (this.speakers.length < 19) {
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
    },
    seekToTime(time) {
      this.$refs.videoPlayer.seekTo(time);
    },
    assignSpeaker(speakerId) {
      if (this.selectedWord) {
        const originalSpeakerId = this.selectedWord.speakerId;
        let found = false;
        
        for (let sentence of this.transcript) {
          for (let word of sentence.words) {
            if (word === this.selectedWord) {
              found = true;
              word.speakerId = speakerId;
              continue;
            }
            if (found) {
              // Если встретили слово с другим спикером или без спикера, прекращаем
              if (word.speakerId !== originalSpeakerId) {
                break;
              }
              word.speakerId = speakerId;
            }
          }
          if (found) {
            break;
          }
        }
        this.selectedWord = null;
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
    async saveAndReload() {
      await this.exportResults();
      // Перезагрузка данных
      const response = await fetch('/api/task');
      if (response.status === 404) {
        alert('Задачи закончились');
        return;
      }
      const data = await response.json();
      this.transcript = data["text"];
      this.videoSrc = data["video"];
      this.file_id = data["file_id"];
      this.speakers = data["speakers"];
      this.channel = data["channel_id"];
      this.$refs.videoPlayer.reset();
    },
    async exportResults() {
      const result = [];
      for (let sentence of this.transcript) {
        for (let word of sentence.words) {
          result.push({
            word: word.word,
            speakerId: word.speakerId || null
          });
        }
      }
      // Отправка на сервер и ожидание ответа
      await fetch('/api/result', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"file_id": this.file_id, "data":result,"channel_id": this.channel,"speakers":this.speakers})
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
