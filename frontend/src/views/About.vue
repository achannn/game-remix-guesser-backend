<template>
  <div class="about">
    <section class="nes-container">
      <p>
        This game is a personal project made by Caleb.
      </p>
      <p>
        He made it after having a really fun night hanging
        out with his girlfriend. One of them would play a videogame
        song on youtube, and the other would try to guess
        what game the song was from.
      </p>
      <p>
        Caleb has a <a href="https://blog.calebjay.com">blog</a>.
      </p>
      <p>
        He also has a
        <a href="https://www.youtube.com/channel/UCR2K9vyQEBb4qUyunijtBHg">
          youtube</a>.
      </p>

    </section>
  </div>
</template>
<style lang="scss">
@import '../colors';
.about {
  display: flex;
  justify-content: center;
  section {
    width: 80vw;
    margin-bottom: 40px;
    text-align: left;
  }
}

a {
  color: $tulipTree;
  text-decoration: underline;
}
</style>
