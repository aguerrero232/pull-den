import { Component, Input, OnInit } from '@angular/core';
import { SpinnerOverlayService } from '../spinner-overlay.service';

@Component({
  selector: 'app-video-recs-display',
  templateUrl: './video-recs-display.component.html',
  styleUrls: ['./video-recs-display.component.css']
})
export class VideoRecsDisplayComponent implements OnInit {

  @Input() usercardrecs: any;
  cards: any;
  video_thumbnail = ['https://sdzwildlifeexplorers.org/sites/default/files/2019-04/animal-hero-echidna.jpg']

  //  TODO: Add way to get recommendations
  video_urls = [
    'https://www.youtube.com/watch?v=Jn_rjC1Rkbs'
  ];


  constructor(private spinnerService: SpinnerOverlayService) {
    // start spinner
    this.spinnerService.show();
    // set a 2 second timer
    setTimeout(() => {
      // stop spinner
      this.spinnerService.hide();
      this.check_recs();

    }, 3000);
  }

  ngOnInit(): void {

  }

  check_recs() {
    this.gets_recs();
  }

  gets_recs() {
    var cards = [
      { title: 'Vid 1', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], description: "video number 1 index 0", channel: "one" },
      { title: 'Vid 2', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], description: "video number 2 index 1", channel: "two" },
      { title: 'Vid 3', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], description: "video number 3 index 2", channel: "three" },
      { title: 'Vid 4', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], description: "video number 4 index 3", channel: "four" },
      { title: 'Vid 5', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], description: "video number 5 index 4", channel: "five" },
      { title: 'Vid 6', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], description: "video number 6 index 5", channel: "six" }
    ];
    this.cards = cards;
  }

}
