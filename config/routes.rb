Rails.application.routes.draw do
resources :home
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html


get '/:id' => "shortener/shortened_urls#show"


end
