export class User {
    constructor(
        public id: string,
        public email: string,
        public video_history: string[],
        public library: string[]
    ) { }
};