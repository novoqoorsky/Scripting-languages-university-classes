Warden::Strategies.add(:password) do
  def valid?
    params['user'] && params['user']['username'] && params['user']['password']
  end

  def authenticate!
    user = User.first(username: params['user']['username'])

    if user.nil?
      throw(:warden, message: 'The username you entered does not exist.')
    elsif user.authenticate(params['user']['password'])
      success!(user)
    else
      throw(:warden, message: 'The username and password combination is incorrect.')
    end
  end
end

class HomePage < Sinatra::Base
  enable :sessions
  register Sinatra::Flash
  set :session_secret, 'supersecret'

  get '/' do
    if env['warden'].authenticated?
      erb :index_logged
    else
      erb :index
    end
  end

  # auth endpoints
  use Warden::Manager do |config|
    config.serialize_into_session(&:id)
    config.serialize_from_session { |id| User.get(id) }
    config.scope_defaults :default, strategies: [:password], action: 'auth/unauthenticated'
    config.failure_app = self
  end

  Warden::Manager.before_failure do |env, _opts|
    env['REQUEST_METHOD'] = 'POST'
    env.each do |key, _value|
      env[key]['_method'] = 'post' if key == 'rack.request.form_hash'
    end
  end

  get '/auth/login' do
    erb :login
  end

  post '/auth/login' do
    env['warden'].authenticate!
    flash[:success] = 'Successfully logged in'
    redirect '/'
  end

  get '/auth/register' do
    erb :register
  end

  post '/auth/register' do
    u = User.new(username: params[:username], email: params[:email],
                 password: params[:password], profile_id: nil)
    u.save
    flash[:success] = 'Successfully created a profile'
    redirect '/profile/registered'
  end

  get '/auth/logout' do
    if env['warden'].authenticated?
      env['warden'].raw_session.inspect
      env['warden'].logout
      flash[:success] = 'Successfully logged out'
    end
    redirect '/'
  end

  post '/auth/unauthenticated' do
    session[:return_to] = env['warden.options'][:attempted_path] if session[:return_to].nil?
    flash[:error] = env['warden.options'][:message] || 'You must log in'
    redirect '/auth/login'
  end


  # profile endpoints
  get '/profile' do
    env['warden'].authenticate!
    erb :'/profile/profile'
  end

  get '/profile/registered' do
    erb :'/profile/profile'
  end

  get '/profile/create' do
    u = env['warden'].user
    if u.profile_id == nil
      p = Profile.new
      p.created_on = Date.today
      p.save
      u.profile_id = p.id
      u.save
    end
    erb :'/profile/create'
  end

  get '/profile/create/finish' do
    redirect '/profile'
  end

  # resolutions endpoints
  get '/resolutions/update' do
    erb :'/resolutions/update'
  end

  get '/resolutions/update/finish' do
    p = Profile.get(env['warden'].user.profile_id)
    p.last_resolutions_update = Date.today
    p.save
    redirect '/profile'
  end

  post '/resolutions/:id/completion' do
    c = Completion.new(resolution_id: params[:id], activity_duration: params[:activity_duration], completed_on: Date.parse(params[:completed_on]))
    c.save
    if Date.parse(params[:completed_on]) < Profile.get(env['warden'].user.profile_id).last_resolutions_update
      flash[:warning] = 'The completion date is before your last confession -
        it means you either forgot about it or are trying to cheat! :('
    else
      flash[:success] = 'Successfully submitted'
    end
    redirect '/resolutions/update'
  end

  get '/resolutions/add' do
    erb :'/resolutions/add'
  end

  post '/resolutions/add' do
    r = Resolution.new(profile_id: env['warden'].user.profile_id,
                       title: params[:title], weekly_frequency: params[:weekly_frequency], activity_duration: params[:activity_duration])
    r.save
    flash[:success] = 'Successfully created a resolution'
    redirect '/profile/create'
  end

  # progress endpoints
  get '/profile/:profile_id/progress/:week_num' do
    erb :'/profile/progress/single_week',
        locals: { week_num: Integer(params[:week_num]) }
  end

end