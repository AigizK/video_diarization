<template>
  <div class="video-player">
    <video
    ref="video"
    :src="videoSrc"
    @timeupdate="onTimeUpdate"
    @error="onVideoError"
  ></video>
    <div class="controls">
      <button @click="playPause">{{ isPlaying ? 'Пауза' : 'Воспроизвести' }}</button>
      <label>
        Скорость:
        <select v-model="playbackRate" @change="changePlaybackRate">
          <option v-for="rate in rates" :key="rate" :value="rate">{{ rate }}x</option>
        </select>
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoPlayer',
  props: ['videoSrc'],
  data() {
    return {
      isPlaying: false,
      playbackRate: 1.0,
      rates: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    };
  },
  methods: {
    playPause() {
      if (this.isPlaying) {
        this.$refs.video.pause();
      } else {
        this.$refs.video.play();
      }
      this.isPlaying = !this.isPlaying;
    },
    changePlaybackRate() {
      this.$refs.video.playbackRate = this.playbackRate;
    },
    setPlaybackRate(rate) {
      this.playbackRate = rate;
      this.changePlaybackRate();
    },
    increasePlaybackRate() {
      const index = this.rates.indexOf(this.playbackRate);
      if (index < this.rates.length - 1) {
        this.playbackRate = this.rates[index + 1];
        this.changePlaybackRate();
      }
    },
    decreasePlaybackRate() {
      const index = this.rates.indexOf(this.playbackRate);
      if (index > 0) {
        this.playbackRate = this.rates[index - 1];
        this.changePlaybackRate();
      }
    },
    seekTo(time) {
      this.$refs.video.currentTime = time;
    },
    onTimeUpdate() {
      this.$emit('timeupdate', this.$refs.video.currentTime);
    },
    reset() {
      this.isPlaying = false;
      this.playbackRate = 1.0;
      if (this.$refs.video) {
        this.$refs.video.pause();
        this.$refs.video.currentTime = 0;
        this.$refs.video.playbackRate = 1.0;
      }
    }
  },
  mounted() {
    // Add event listeners to sync playing state
    this.$refs.video.addEventListener('play', () => {
      this.isPlaying = true;
    });
    this.$refs.video.addEventListener('pause', () => {
      this.isPlaying = false;
    });
  }
};
</script>

<style>
.video-player {
  max-width: 480px;
  width: 100%;
  margin: 0 auto;
}
video {
  width: 100%;
  height: auto;
}
.controls {
  margin-top: 10px;
}
</style>

