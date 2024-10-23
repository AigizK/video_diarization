<template>
  <div class="save-result">
    <button @click="showConfirmation" class="save-button">Сохранить</button>
    
    <div v-if="showPopup" class="popup-overlay">
      <div class="popup">
        <p>Вы уверены что закончили все работы? После нажатия ДА, эти данные будут сохранены, и вы получите новую задачу.</p>
        <div class="popup-buttons">
          <button @click="confirmSave">ДА</button>
          <button @click="closePopup">НЕТ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SaveResult',
  data() {
    return {
      showPopup: false
    }
  },
  methods: {
    showConfirmation() {
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
    },
    confirmSave() {
      this.$emit('save-and-reload');
      this.showPopup = false;
    }
  }
}
</script>

<style scoped>
.save-result {
  margin: 20px 0;
}

.save-button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  max-width: 400px;
  text-align: center;
}

.popup-buttons {
  margin-top: 20px;
}

.popup-buttons button {
  margin: 0 10px;
  padding: 8px 20px;
  cursor: pointer;
}
</style>
