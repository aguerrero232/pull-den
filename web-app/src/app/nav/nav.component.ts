import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  login() {
    this.router.navigate(['/login']);
  }

  logout() {
    this.router.navigate(["/logout"]);
  }

  signup() {
    this.router.navigate(["/sign-up"]);
  }

  openDownload(content: any) {
    this.modalService.open(content);
  }

  constructor(private breakpointObserver: BreakpointObserver, private router: Router, private modalService: NgbModal) { }

}
