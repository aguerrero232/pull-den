import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { User } from './user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: any;
  userSub = new Subject<User>();

  constructor() {
    this.userSub.subscribe(u => this.user = u);
  }

  setUser() {
    this.userSub.next(this.user);
  }

  getUser() {
    return this.user;
  }

  getUserID(id: string) {

  }

  async addUser(user: User) {
  }

  async updateUser(updatedUser: User) {
  }

  onUserChange(): Observable<any> {
    return this.userSub.asObservable();
  }
}