<template>
  <div class="hotkeys-info">
    <h3>Горячие клавиши:</h3>
    <ul>
      <li>Цифры 1-9: выбор спикера</li>
      <li>0: удалить спикера</li>
      <li>Пробел: пауза/воспроизведение видео</li>
      <li>"+" / "-": ускорение/замедление видео</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HotkeysInfo'
};
</script>

<style>
.hotkeys-info {
  margin-top: 20px;
}
</style>

