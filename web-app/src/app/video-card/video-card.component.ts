import { Component, Input, OnInit } from '@angular/core';


@Component({
  selector: 'app-video-card',
  templateUrl: './video-card.component.html',
  styleUrls: ['./video-card.component.css']
})
export class VideoCardComponent implements OnInit {
  // @ inuput card object
  @Input() card: any;

  constructor() { }
  ngOnInit(): void {

  }

}
