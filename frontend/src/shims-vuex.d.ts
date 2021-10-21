import { Store } from '@/store';// path to store file
import { State } from './store/index';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $store: Store<State>;
  }
}
