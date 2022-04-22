import { Injectable } from '@angular/core';
import { Overlay, OverlayRef } from '@angular/cdk/overlay';
import { ComponentPortal } from '@angular/cdk/portal';
import { SpinnerOverlayComponent } from './spinner-overlay/spinner-overlay.component';

@Injectable({
  providedIn: 'root'
})
export class SpinnerOverlayService {


  private overlayRef: OverlayRef | undefined;

  constructor(private overlay: Overlay) { }

  public show(): void {
    if (!this.overlayRef) {
      this.overlayRef = this.overlay.create();
    }
    const spinnerOverlayPortal = new ComponentPortal(SpinnerOverlayComponent);
    this.overlayRef.attach(spinnerOverlayPortal);

  }

  public hide(): void {
    if (this.overlayRef) {
      this.overlayRef.detach();
    }
  }
}