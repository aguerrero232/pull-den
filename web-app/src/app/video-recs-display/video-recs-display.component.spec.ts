import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoRecsDisplayComponent } from './video-recs-display.component';

describe('VideoRecsDisplayComponent', () => {
  let component: VideoRecsDisplayComponent;
  let fixture: ComponentFixture<VideoRecsDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VideoRecsDisplayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VideoRecsDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
