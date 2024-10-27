<template>
  <div class="speaker-list">
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Имя</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="speaker in speakers" :key="speaker.id">
          <td data-label="ID">{{ speaker.id }}</td>
          <td data-label="Имя">
            <input type="text" v-model="speaker.name" @input="updateName(speaker.id, speaker.name)" />
          </td>
          <td data-label="Действия">
            <button @click="removeSpeaker(speaker.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button @click="addSpeaker" :disabled="speakers.length >= 50">Добавить спикера</button>
  </div>
</template>

<script>
export default {
  name: 'SpeakerList',
  props: ['speakers'],
  methods: {
    addSpeaker() {
      this.$emit('addSpeaker');
    },
    removeSpeaker(speakerId) {
      this.$emit('removeSpeaker', speakerId);
    },
    updateName(speakerId, newName) {
      this.$emit('updateSpeakerName', speakerId, newName);
    }
  }
};
</script>

<style scoped>
.speaker-list {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
input[type="text"] {
  width: 100%;
  padding: 5px;
  box-sizing: border-box;
}
button {
  margin-top: 10px;
}

@media screen and (max-width: 600px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }
  thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }
  tr {
    border: 1px solid #ccc;
    margin-bottom: 10px;
  }
  td {
    border: none;
    position: relative;
    padding-left: 50%;
  }
  td:before {
    content: attr(data-label);
    position: absolute;
    left: 6px;
    width: 45%;
    padding-right: 10px;
    white-space: nowrap;
    font-weight: bold;
  }
}
</style>