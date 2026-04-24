export class Document {
  constructor(
    public name: string,
    public pages?: number,
    public chunks?: number,
    public uploadDate: Date = new Date()
  ) {}

  get displayName(): string {
    return this.name.length > 40 ? this.name.substring(0, 37) + '...' : this.name;
  }

  get summary(): string {
    return `${this.pages || '?'} pages · ${this.chunks || '?'} chunks`;
  }
}