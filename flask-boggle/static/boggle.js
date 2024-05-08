class EachGame{
    constructor(boardId, secs = 60) {
      this.secs = secs; 
    this.displayTimer();

    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);

    this.timer = setInterval(this.tick.bind(this), 1000);

    $(".post-word", this.board).on("submit", this.wordExam.bind(this));
    }
    // display a message notification if necessary and then removing it in order to possibly display another one
    displayMessage(noti, cls){
        $(".noti", this.board)
      .text(noti)
      .removeClass()
      .addClass(`noti ${cls}`);
    }
    
    async wordExam(evt) { 
        evt.preventDefault();
        const $word = $("word", this.board);
        let word = $word.val();
    
        if (!word) return;

    if (this.words.has(word)) {
      this.displayMessage(`${word} already exists`, "err");
      return;
    }
    
    const response = await axios.get("/check-valid", {params: word, word })
    if (response.data.result === "not-word") {
        this.displayMessage(`${word} is not a valid English word`, "err");
      } else if (response.data.result === "not-on-board") {
        this.displayMessage(`${word} is not a valid word on this board`, "err");
      } else {
        this.displayWord(word);
        this.score += word.length;
        this.displayScore();
        this.words.add(word);
        this.displayMessage(`Added: ${word}`, "ok");
      }
  
      $word.val("").focus();
    }

    displayWord(word) {
      $(".word-list", this.board).append($("<li>", { text: word }));
    }

    displayScore() {
      $(".score", this.board).text(this.score);
    }

    displayTimer() {
      $(".timer", this.board).text(this.secs);
    }
  
  
    async tick() {
      this.secs -= 1;
      this.displayTimer();
  
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }

    async scoreGame() {
      $(".add-word", this.board).hide();
      const response = await axios.post("/post-score", { score: this.score });
      if (response.data.brokeRecord) {
        this.displayMessage(`New record: ${this.score}`, "ok");
      } else {
        this.displayMessage(`Final score: ${this.score}`, "ok");
      }
    }
  
    }

