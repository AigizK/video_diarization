<template>
  <div class="transcription">
    <div v-for="(sentence, index) in transcript" :key="index" class="sentence">
      <span
        v-for="(word, idx) in sentence.words"
        :key="idx"
        :class="{
          'current-word': isCurrentWord(word),
          'selected-word': word === selectedWord,
        }"
        :style="{ backgroundColor: getSpeakerColor(word.speakerId) }"
        @click="selectWord(word)"
      >
        {{ word.word }}
      </span>
    </div>
    <div v-if="selectedWord" class="speaker-buttons">
      <button
        v-for="speaker in speakers"
        :key="speaker.id"
        :style="{backgroundColor: speaker.color}"
        @click="assignSpeaker(speaker.id)"
      >
        {{ speaker.name }}
      </button>
      <button @click="assignSpeaker(null)">Удалить спикера</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Transcription',
  props: ['transcript', 'speakers', 'currentTime'],
  data() {
    return {
      currentWord: null,
      selectedWord: null
    };
  },
  watch: {
  currentTime() {
    // Обновляем компонент при изменении времени
  },
},
  methods: {
    selectWord(word) {
      this.selectedWord = word;
      this.$emit('selectWord', word);
    },
    assignSpeaker(speakerId) {
      this.$emit('assignSpeaker', speakerId);
      this.selectedWord = null;
    },
    isCurrentWord(word) {
      return this.currentTime >= word.start && this.currentTime <= word.end;
    },
    getSpeakerColor(speakerId) {
      const speaker = this.speakers.find(s => s.id === speakerId);
      return speaker ? speaker.color : 'transparent';
    }
  }
};
</script>

<style>
.transcription {
  margin-top: 20px;
}
.sentence {
  margin-bottom: 10px;
}
.sentence span {
  margin-right: 5px;
  cursor: pointer;
}
.current-word {
  font-weight: bold;
}
.speaker-buttons {
  margin-top: 10px;
}
.speaker-buttons button {
  margin-right: 5px;
  color: #fff;
}

.current-word {
  text-decoration: underline;
}
</style>

