import { Component, Input, OnInit } from '@angular/core';
import { map } from 'rxjs/operators';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';

@Component({
  selector: 'app-video-recs-display',
  templateUrl: './video-recs-display.component.html',
  styleUrls: ['./video-recs-display.component.css']
})
export class VideoRecsDisplayComponent implements OnInit {

  @Input() usercardrecs: any;

  ngOnInit(): void {
  }

  video_thumbnail = ['https://sdzwildlifeexplorers.org/sites/default/files/2019-04/animal-hero-echidna.jpg']

  //  TODO: Add way to get recommendations
  video_urls = [
    'https://www.youtube.com/watch?v=Jn_rjC1Rkbs'
  ];


  /** Based on the screen size, switch from standard to one column per row */
  cards = [
    { title: 'Vid 1', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], channel: "one" },
    { title: 'Vid 2', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], channel: "two" },
    { title: 'Vid 3', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], channel: "three" },
    { title: 'Vid 4', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], channel: "four" },
    { title: 'Vid 5', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], channel: "five" },
    { title: 'Vid 6', link: this.video_urls[0], thumbnail: this.video_thumbnail[0], channel: "six" }
  ];
  constructor(private breakpointObserver: BreakpointObserver) {
    this.check_recs();
  }

  check_recs() {
    if (this.usercardrecs)
      return true;
    return false;
  }
}
